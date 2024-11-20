import { Component } from '@angular/core';

@Component({
  selector: 'app-tips-enf-renal',
  templateUrl: './tips-enf-renal.page.html',
  styleUrls: ['./tips-enf-renal.page.scss'],
})
export class TipsEnfRenalPage {
  isModalOpen = false;
  modalTitle = '';
  modalContent = '';
  modalImageUrl = '';

  openModal(title: string, content: string, imageUrl: string) {
    this.modalTitle = title;
    this.modalContent = content;
    this.modalImageUrl = imageUrl;
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
  }
}