import { Component } from '@angular/core';
import { Storage } from '@ionic/storage-angular';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {
  // Definir la propiedad formData como un objeto
  formData: any = {
    peso: '',
    distribucionGrasa: '',
    antecedentesFamiliares: '',
    edad: '',
    prediabetes: '',
    alimentacion: ''
  };

  private _storage: Storage | null = null;

  // Constructor con el servicio de almacenamiento
  constructor(private storage: Storage) {
    this.init();
  }

  // Inicializar el almacenamiento local
  async init() {
    const storage = await this.storage.create();
    this._storage = storage;
  }

  // Método submitForm que se llamará al enviar el formulario
  submitForm() {
    console.log('Datos del formulario:', this.formData);
    // Guardar los datos en el almacenamiento local
    this._storage?.set('formData', this.formData);
  }
}
