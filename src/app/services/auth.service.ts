import { Injectable } from '@angular/core';
import { 
  HttpClient, 
  HttpHeaders, 
  HttpErrorResponse,
  HttpResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError, map } from 'rxjs/operators';
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
  user?: {
    id: number;
    username: string;
    full_name: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private token: string | null = null;
  private baseUrl = 'ec2-35-174-114-42.compute-1.amazonaws.com:5000';

  constructor(private http: HttpClient) {}

  register(userData: RegisterUser): Observable<AuthResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
  
    console.log('Enviando datos de registro:', userData);
    console.log('URL de registro:', `${this.apiUrl}/register`);

    return this.http.post<AuthResponse>(`${this.apiUrl}/register`, userData, { 
      headers,
      observe: 'response'
    }).pipe(
      map((response: HttpResponse<AuthResponse>) => {
        const body = response.body;
        if (body && body.token) {
          this.setToken(body.token);
        }
        return body as AuthResponse;
      }),
      tap(response => {
        console.log('Respuesta del servidor:', response);
      }),
      catchError((error) => {
        console.error('Error durante el registro:', error);
        return throwError(() => new Error('Error en el proceso de registro.'));
      })
    );
  }

  login(loginData: LoginUser): Observable<AuthResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, loginData, { 
      headers,
      observe: 'response'
    }).pipe(
      map((response: HttpResponse<AuthResponse>) => {
        const body = response.body;
        
        if (body && body.token) {
          this.setToken(body.token);
        }
        
        return body as AuthResponse;
      }),
      catchError(this.handleError)
    );
  }

  // Método para manejar errores de HTTP
  private handleError(error: HttpErrorResponse) {
    console.error('Error completo:', error);
    
    // Error de red o conexión
    if (error.status === 0) {
      return throwError(() => ({
        error: true,
        message: 'No se pudo conectar con el servidor. Verifique su conexión a internet.'
      }));
    }
    
    // Errores del servidor
    if (error.error instanceof ErrorEvent) {
      // Error del lado del cliente
      return throwError(() => ({
        error: true,
        message: error.error.message || 'Error de cliente desconocido'
      }));
    }
    
    // Error del lado del servidor
    let errorMessage = 'Error desconocido del servidor';
    if (error.error && error.error.message) {
      errorMessage = error.error.message;
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    return throwError(() => ({
      error: true,
      message: errorMessage,
      status: error.status
    }));
  }

  getToken(): string | null {
    return this.token || localStorage.getItem('token');
  }

  public setToken(token: string): void {
    this.token = token;
    localStorage.setItem('authToken', token);
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('token');
  }

  verifyToken(): Observable<AuthResponse> {
    const token = this.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    return this.http.get<AuthResponse>(`${this.apiUrl}/verify-token`, { 
      headers,
      observe: 'response'
    }).pipe(
      map((response: HttpResponse<AuthResponse>) => {
        const body = response.body;
        return body as AuthResponse;
      }),
      catchError(this.handleError)
    );
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}