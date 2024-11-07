import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment'; // Asegúrate de que la ruta sea correcta

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
        })
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
        })
      );
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
    return this.http.get<AuthResponse>(`${this.apiUrl}/verify-token`, { headers });
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}
