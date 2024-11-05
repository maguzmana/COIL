import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage-angular';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private TOKEN_KEY = 'auth_token';
  private _storage: Storage | null = null;

  constructor(private storage: Storage) {
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
}