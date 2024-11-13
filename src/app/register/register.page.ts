import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { NavController, AlertController } from '@ionic/angular';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage {
  registerForm: any = {
    full_name: '',
    username: '',
    password: '',
    weight: '',
    height: '',
    age: '',
    gender: '',
    goal: '',
    physical_activity_level: '',
    health_conditions: ''
  };
  currentStep: number = 1;

  constructor(
    private authService: AuthService,
    private navCtrl: NavController,
    private alertController: AlertController
  ) {}

  nextStep() {
    if (this.currentStep === 1) {
      // Validar información básica aquí si es necesario
      this.currentStep = 2;
    }
  }

  prevStep() {
    if (this.currentStep === 2) {
      this.currentStep = 1;
    }
  }

  async onRegister() {
    if (this.currentStep === 2) {
      this.authService.register(this.registerForm).subscribe({
        next: async (response) => {
          const alert = await this.alertController.create({
            header: 'Registro exitoso',
            message: response.message,
            buttons: ['OK']
          });
          await alert.present();
          this.navCtrl.navigateRoot('/login'); // Navega a la pantalla de login
        },
        error: async (err) => {
          const alert = await this.alertController.create({
            header: 'Error en el registro',
            message: err.error.error || 'Error desconocido',
            buttons: ['OK']
          });
          await alert.present();
        }
      });
    } else {
      const alert = await this.alertController.create({
        header: 'Formulario incompleto',
        message: 'Por favor, completa todos los campos.',
        buttons: ['OK']
      });
      await alert.present();
    }
  }
}