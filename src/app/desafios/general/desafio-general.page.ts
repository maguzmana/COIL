import { Component } from '@angular/core';

@Component({
  selector: 'app-desafio-general',
  templateUrl: './desafio-general.page.html',
  styleUrls: ['./desafio-general.page.scss'],
})
export class DesafioGeneralPage {
  desafioGeneral = {
    titulo: 'Desafío de Vida Saludable',
    descripcion: 'Un desafío que combina ejercicio, buena alimentación y descanso.',
    imagen: 'assets/img/general.jpg',
    puntos: 50,
  };

  constructor() {}

  completarDesafio() {
    alert(`¡Felicidades! Has completado el desafío general. Ganaste ${this.desafioGeneral.puntos} puntos.`);
  }
}