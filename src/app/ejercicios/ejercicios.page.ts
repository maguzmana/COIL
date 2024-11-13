import { Component} from '@angular/core';

@Component({
  selector: 'app-ejercicios',
  templateUrl: './ejercicios.page.html',
  styleUrls: ['./ejercicios.page.scss'],
})
export class EjerciciosPage{

  ejercicios = [
    { name: 'Parte Superior Del Cuerpo', 
      duration: '60 Minutos', 
      calories: '1320 Cal', 
      image: 'assets/estiramiento2.jpg' 
    },
    { name: 'Estiramiento De Cuerpo Completo', 
      duration: '45 Minutos', 
      calories: '1450 Cal', 
      image: 'assets/estirar1.jpg' 
    },
    {
      name: 'Trotar',
      duration: '30 min',
      calories: '300 cal.',
      image: 'assets/cardio.jpg', 
    },
    {
      name: 'Andar en Bicicleta',
      duration: '60 min',
      calories: '550 cal.',
      image: 'assets/fuerza.jpg',
    }
  ];

  constructor() { }

}
