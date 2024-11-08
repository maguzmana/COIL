/* login.page.ts */

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { LoadingController, AlertController } from '@ionic/angular';
import { AuthService } from '../services/auth.service'; // Cambia esto por la ruta correcta

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
  credentials = {
    username: '',
    password: ''
  };

  constructor(
    private authService: AuthService, // Usa AuthService en lugar de UserService
    private router: Router,
    private loadingController: LoadingController,
    private alertController: AlertController
  ) {}

  async onLogin() {
    const loading = await this.loadingController.create({
      message: 'Iniciando sesión...',
      spinner: 'crescent'
    });
    await loading.present();

    // Aquí se asume que el login siempre es exitoso
    this.authService.setToken('fake-token'); // Establece un token ficticio
    loading.dismiss();
    this.router.navigate(['/tabs/tab2']);
  }

  async showAlert(header: string, message: string) {
    const alert = await this.alertController.create({
      header,
      message,
      buttons: ['OK']
    });
    await alert.present();
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }
}