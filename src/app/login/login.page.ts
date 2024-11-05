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
    if (!this.credentials.username || !this.credentials.password) {
      await this.showAlert('Error', 'Por favor, completa todos los campos.');
      return;
    }

    const loading = await this.loadingController.create({
      message: 'Iniciando sesión...',
      spinner: 'crescent'
    });
    await loading.present();

    try {
      this.authService.login(this.credentials).subscribe(
        (response: any) => {
          loading.dismiss();
          if (response.token) {
            this.authService.setToken(response.token);
            this.router.navigate(['/tabs/tab2']);
          } else {
            this.showAlert('Error', 'Respuesta inválida del servidor');
          }
        },
        async (error) => {
          loading.dismiss();
          console.error('Error al iniciar sesión:', error);
          await this.showAlert('Error', 'Usuario o contraseña incorrectos');
        }
      );
    } catch (error) {
      loading.dismiss();
      console.error('Error al iniciar sesión:', error);
      await this.showAlert('Error', 'Ocurrió un error al intentar iniciar sesión');
    }
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