import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-tips-enf-renal',
  templateUrl: './tips-enf-renal.page.html',
  styleUrls: ['./tips-enf-renal.page.scss'],
})
export class TipsEnfRenalPage implements OnInit {
  isModalOpen = false; // Controla si el modal está abierto o cerrado
  modalTitle = ''; // Título del modal
  modalContent = ''; // Contenido dinámico del modal

  constructor() {}

  ngOnInit() {}

  // Abre el modal con título y contenido dinámico
  openModal(title: string, content: string) {
    this.modalTitle = title;
    this.modalContent = content;
    this.isModalOpen = true; // Abre el modal
  }

  // Cierra el modal
  closeModal() {
    this.isModalOpen = false;
  }
}
