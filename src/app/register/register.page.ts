/* register.page.ts */

import { Component } from '@angular/core';
import { NavController } from '@ionic/angular';
import { UserService } from '../services/user.service';
import { AuthService } from '../services/auth.service';
import { AlertController } from '@ionic/angular';

// Interfaz para el formulario (con valores que pueden ser null)
interface UserForm {
  fullName: string;
  username: string;
  password: string;
  weight: number | null;
  height: number | null;
  age: number | null;
  gender: string;
  goal: string;
  physicalActivityLevel: number | null;
  healthConditions: string[];
}

// Interfaz para el registro (sin valores null)
interface RegisterUser {
  fullName: string;
  username: string;
  password: string;
  weight: number;
  height: number;
  age: number;
  gender: string;
  goal: string;
  physicalActivityLevel: number;
  healthConditions: string[]; // Cambiado a string[]
}

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage {
  user: UserForm = {
    fullName: '',
    username: '',
    password: '',
    weight: null,
    height: null,
    age: null,
    gender: '',
    goal: '',
    physicalActivityLevel: null,
    healthConditions: []
  };

  constructor(
    private navCtrl: NavController,
    private userService: UserService,
    private authService: AuthService,
    private alertController: AlertController,
  ) {}

  async onRegister() {
    if (this.validateForm()) {
      try {
        const userData: RegisterUser = {
          fullName: this.user.fullName,
          username: this.user.username,
          password: this.user.password,
          weight: this.user.weight!,
          height: this.user.height!,
          age: this.user.age!,
          gender: this.user.gender,
          goal: this.user.goal,
          physicalActivityLevel: this.user.physicalActivityLevel!,
          healthConditions: this.user.healthConditions
        };
  
        console.log('Datos que se enviarán al servidor:', userData);
  
        this.authService.register(userData).subscribe({
          next: (response) => {
            console.log('Respuesta del servidor:', response);
  
            if (response && response.token) {
              this.authService.setToken(response.token);
              this.presentSuccessAlert('Registro exitoso');
              this.navCtrl.navigateForward('/login');
            } else {
              this.presentErrorAlert('No se recibió un token de autenticación');
            }
          },
          error: (error) => {
            console.error('Error completo:', error);
            this.handleRegistrationError(error);
          }
        });
      } catch (error) {
        console.error('Error inesperado:', error);
        this.presentErrorAlert('Ocurrió un error inesperado. Intente nuevamente.');
      }
    } else {
      this.presentErrorAlert('Por favor, completa todos los campos obligatorios.');
    }
  }

  private handleRegistrationError(error: any) {
    let errorMessage = 'Error en el registro';

    if (error.error && error.error.message) {
      errorMessage = error.error.message;
    } else if (error.message) {
      errorMessage = error.message;
    }

    this.presentErrorAlert(errorMessage);
  }

  async presentSuccessAlert(message: string) {
    const alert = await this.alertController.create({
      header: 'Registro Exitoso',
      message: message,
      buttons: ['OK']
    });

    await alert.present();
  }

  async presentErrorAlert(message: string) {
    const alert = await this.alertController.create({
      header: 'Error de Registro',
      message: message,
      buttons: ['OK']
    });

    await alert.present();
  }


  validateForm(): boolean {
    return !!(
      this.user.fullName &&
      this.user.fullName.trim() &&
      this.user.username &&
      this.user.username.trim() &&
      this.user.password &&
      this.user.password.trim() &&
      this.user.weight &&
      this.user.weight > 0 &&
      this.user.height &&
      this.user.height > 0 &&
      this.user.age &&
      this.user.age > 0 &&
      this.user.gender &&
      this.user.goal &&
      this.user.physicalActivityLevel !== null
    );
  }

  goToLogin() {
    this.navCtrl.navigateForward('/login');
  }

  isFieldValid(field: keyof UserForm): boolean {
    if (field === 'weight' || field === 'height' || field === 'age' || field === 'physicalActivityLevel') {
      return this.user[field] !== null && this.user[field]! > 0;
    }
    if (typeof this.user[field] === 'string') {
      return (this.user[field] as string).trim().length > 0;
    }
    return !!this.user[field];
  }

  onNumberInput(event: any, field: 'weight' | 'height' | 'age' | 'physicalActivityLevel') {
    const value = event.target.value;
    if (value === '' || value === null) {
      this.user[field] = null;
    } else {
      const numValue = parseFloat(value);
      this.user[field] = numValue > 0 ? numValue : null;
    }
  }

  onHealthConditionChange(condition: string) {
    const index = this.user.healthConditions.indexOf(condition);
    if (index === -1) {
      this.user.healthConditions.push(condition);
    } else {
      this.user.healthConditions.splice(index, 1);
    }
  }

  resetForm() {
    this.user = {
      fullName: '',
      username: '',
      password: '',
      weight: null,
      height: null,
      age: null,
      gender: '',
      goal: '',
      physicalActivityLevel: null,
      healthConditions: []
    };
  }
}