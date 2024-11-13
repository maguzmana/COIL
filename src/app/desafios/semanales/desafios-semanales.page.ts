import { Component } from '@angular/core';

@Component({
  selector: 'app-desafios-semanales',
  templateUrl: './desafios-semanales.page.html',
  styleUrls: ['./desafios-semanales.page.scss'],
})
export class DesafiosSemanalesPage {
  desafios = [
    {
      id: 1,
      titulo: 'Campeón del Movimiento',
      subtitulo: '30 minutos de ejercicio',
      descripcion: 'Realiza 30 minutos de actividad física, como bailar, caminar, correr o yoga.',
      imagen: 'assets/img/campeon.jpg',
      duracion: '30 minutos',
      calorias: '12 Kcal',
      nivel: 'Principiante',
      puntos: 20,
      bonus: 10,
    },
    // Puedes agregar más desafios aquí
  ];

  constructor() {}

  verDetalles(id: number) {
    console.log('Desafío seleccionado:', id);
  }

  completarDesafio(desafio: any) {
    // Aquí puedes manejar la lógica de completar el desafío
    alert(`¡Felicidades! Has completado el desafío: ${desafio.titulo}. Ganaste ${desafio.puntos} puntos.`);
  }
}