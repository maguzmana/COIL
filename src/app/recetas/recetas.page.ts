/* recetas.page.ts */

import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-recetas',
  templateUrl: './recetas.page.html',
  styleUrls: ['./recetas.page.scss'],
})
export class RecetasPage {

  recetas = [
    { 
      name: 'Smoothie Frutal', 
      duration: '10 Minutos', 
      calories: '120 Cal', 
      image: 'assets/smoothie.jpg' 
    },
    { 
      name: 'Ensalada Con Quinoa', 
      duration: '20 Minutos', 
      calories: '150 Cal', 
      image: 'assets/ensalada.jpg' 
    },
    { 
      name: 'Tostadas de Aguacate', 
      duration: '15 Minutos', 
      calories: '200 Cal', 
      image: 'assets/pan.jpg' 
    },
    { 
      name: 'Sopa de Lentejas', 
      duration: '30 Minutos', 
      calories: '180 Cal', 
      image: 'assets/sopa.jpg' 
    },
    { 
      name: 'Pasta al Pesto', 
      duration: '25 Minutos', 
      calories: '300 Cal', 
      image: 'assets/pasta.jpg' 
    },
  ];

  constructor() { }

}
