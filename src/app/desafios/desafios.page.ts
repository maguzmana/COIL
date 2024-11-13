import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-challenges',
  templateUrl: './desafios.page.html',
  styleUrls: ['./desafios.page.scss'],
})
export class DesafiosPage{
  desafios = [
    {
      id: 1,
      titulo: 'Reto de Hidratación',
      subtitulo: 'Mantente hidratado por 7 días',
      descripcion: 'Bebe al menos 2 litros de agua al día durante una semana.',
      imagen: 'assets/img/hidratacion.jpg'
    },
    {
      id: 2,
      titulo: 'Reto de Ejercicio',
      subtitulo: '30 minutos de ejercicio diario',
      descripcion: 'Realiza 30 minutos de actividad física al día.',
      imagen: 'assets/img/ejercicio.jpg'
    },
    {
      id: 3,
      titulo: 'Reto de Sueño',
      subtitulo: '8 horas de sueño',
      descripcion: 'Asegúrate de dormir al menos 8 horas cada noche.',
      imagen: 'assets/img/sueno.jpg'
    }
  ];

  constructor() {}

  verDetalles(id: number) {
    console.log('Desafío seleccionado:', id);
  }
}
