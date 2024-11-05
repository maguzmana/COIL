/* tab3.page.ts */

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../services/user.service';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page implements OnInit {
  profileForm: FormGroup;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private toastController: ToastController
  ) {
    this.profileForm = this.fb.group({
      fullName: ['', Validators.required],
      weight: ['', [Validators.required, Validators.min(0)]],
      height: ['', [Validators.required, Validators.min(0)]],
      age: ['', [Validators.required, Validators.min(0)]],
      gender: ['', Validators.required],
      goal: ['', Validators.required],
      physicalActivityLevel: ['', [Validators.required, Validators.min(0)]],
      healthConditions: [''],
      password: [''],
      confirmPassword: ['']
    });
  }

  ngOnInit() {
    this.loadProfile();
  }

  async loadProfile() {
    try {
      const profile = await this.userService.getProfile().toPromise();
      this.profileForm.patchValue(profile.user);
    } catch (error) {
      this.showToast('Error al cargar el perfil');
    }
  }

  async onSubmit() {
    if (this.profileForm.valid) {
      this.loading = true;
      try {
        const formData = this.profileForm.value;
        if (!formData.password) {
          delete formData.password;
          delete formData.confirmPassword;
        } else if (formData.password !== formData.confirmPassword) {
          this.showToast('Las contraseñas no coinciden');
          return;
        }
        
        await this.userService.updateProfile(formData).toPromise();
        this.showToast('Perfil actualizado exitosamente');
      } catch (error) {
        this.showToast('Error al actualizar el perfil');
      } finally {
        this.loading = false;
      }
    }
  }

  async showToast(message: string) {
    const toast = await this.toastController.create({
      message,
      duration: 2000,
      position: 'bottom'
    });
    toast.present();
  }
}