import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private TOKEN_KEY = 'auth_token';
  private _storage: Storage | null = null;
  private apiUrl = environment.apiUrl; // Asegúrate de tener esta variable en tu archivo de entorno

  constructor(private storage: Storage, private http: HttpClient) {
    this.init();
  }

  async init() {
    if (this._storage === null) {
      this._storage = await this.storage.create();
    }
  }

  async setToken(token: string) {
    await this._storage?.set(this.TOKEN_KEY, token);
  }

  async getToken(): Promise<string | null> {
    return await this._storage?.get(this.TOKEN_KEY) || null;
  }

  async removeToken() {
    await this._storage?.remove(this.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  private getHeaders(): HttpHeaders {
    const token = this.getToken();
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
  }

  getProfile(): Observable<any> {
    return this.http.get(`${this.apiUrl}/profile`, { headers: this.getHeaders() });
  }

  updateProfile(profileData: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/update-profile`, profileData, { headers: this.getHeaders() });
  }
}