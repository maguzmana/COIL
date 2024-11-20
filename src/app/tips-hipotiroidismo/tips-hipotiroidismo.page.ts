import { Component } from '@angular/core';

@Component({
  selector: 'app-tips-hipotiroidismo',
  templateUrl: './tips-hipotiroidismo.page.html',
  styleUrls: ['./tips-hipotiroidismo.page.scss'],
})
export class TipsHipotiroidismoPage {
  isModalOpen: boolean = false; // Controla si el modal está abierto o cerrado
  modalTitle: string = ''; // Título del modal
  modalContent: string = ''; // Contenido del modal

  constructor() {}

  // Método para abrir el modal y pasarle el título y contenido
  openModal(title: string, content: string) {
    this.modalTitle = title;
    this.modalContent = content;
    this.isModalOpen = true; // Abre el modal
  }

  // Método para cerrar el modal
  closeModal() {
    this.isModalOpen = false; // Cierra el modal
  }
}
