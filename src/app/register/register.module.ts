import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'; // Agregar ReactiveFormsModule
import { IonicModule } from '@ionic/angular';
import { RegisterPage } from './register.page';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule, // Importar ReactiveFormsModule aquí
    HttpClientModule,
    IonicModule,
    RouterModule.forChild([{ path: '', component: RegisterPage }])
  ],
  declarations: [RegisterPage]
})
export class RegisterPageModule {}
