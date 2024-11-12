import { Component } from '@angular/core';

@Component({
  selector: 'app-progreso',
  templateUrl: './progreso.page.html',
  styleUrls: ['./progreso.page.scss'],
})
export class ProgresoPage {
  selectedDate: string;

  constructor() {
    this.selectedDate = new Date().toISOString(); // Valor inicial
  }
}
