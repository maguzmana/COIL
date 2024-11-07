import { Injectable } from '@angular/core';
import { 
  HttpClient, 
  HttpHeaders, 
  HttpErrorResponse 
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

// Interfaces para tipar los datos
export interface RegisterUser {
  fullName: string;
  username: string;
  password: string;
  weight: number;
  height: number;
  age: number;
  gender: string;
  goal: string;
  physicalActivityLevel: number;
  healthConditions: string[];
}

export interface LoginUser {
  username: string;
  password: string;
}

export interface AuthResponse {
  token?: string;
  message?: string;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private token: string | null = null;

  constructor(private http: HttpClient) {}

  register(userData: RegisterUser): Observable<AuthResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post<AuthResponse>(`${this.apiUrl}/register`, userData, { headers })
      .pipe(
        tap(response => {
          console.log('Respuesta del servidor:', response);
          if (response.token) {
            this.setToken(response.token);
          }
        }),
        catchError(this.handleError)
      );
  }

  login(loginData: LoginUser): Observable<AuthResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, loginData, { headers })
      .pipe(
        tap(response => {
          if (response.token) {
            this.setToken(response.token);
          }
        }),
        catchError(this.handleError)
      );
  }

  // Método para manejar errores de HTTP
  private handleError(error: HttpErrorResponse) {
    console.error('Error completo:', error);
    
    if (error.status === 0) {
      // Error de conexión
      return throwError(() => new Error('No se pudo conectar con el servidor. Verifique su conexión.'));
    }
    
    // Si el servidor devolvió un error
    const errorMessage = error.error?.message || 'Error desconocido del servidor';
    return throwError(() => ({ 
      error: true, 
      message: errorMessage 
    }));
  }

  getToken(): string | null {
    return this.token || localStorage.getItem('token');
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('token', token);
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('token');
  }

  verifyToken(): Observable<AuthResponse> {
    const token = this.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<AuthResponse>(`${this.apiUrl}/verify-token`, { headers })
      .pipe(
        catchError(this.handleError)
      );
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}