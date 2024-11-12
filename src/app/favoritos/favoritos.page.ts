// favoritos.page.ts
import { Component } from '@angular/core'; // Elimina OnInit si no lo vas a usar

interface Comida {
  id: number;
  nombre: string;
  calorias: number;
  imagen: string;
}

interface Ejercicio {
  id: number;
  nombre: string;
  duracion: string;
  calorias: number;
  imagen: string;
}

@Component({
  selector: 'app-favoritos',
  templateUrl: './favoritos.page.html',
  styleUrls: ['./favoritos.page.scss'],
})
export class FavoritosPage { // Elimina implements OnInit
  comidasFavoritas: Comida[] = [
    {
      id: 1,
      nombre: 'Ensalada César',
      calorias: 250,
      imagen: 'assets/images/ensaladacesar.png'
    },
    {
      id: 2,
      nombre: 'Pollo a la plancha',
      calorias: 165,
      imagen: 'assets/images/pollo-plancha.jpg'
    }
  ];

  ejerciciosFavoritos: Ejercicio[] = [
    {
      id: 1,
      nombre: 'Caminata',
      duracion: '30 minutos',
      calorias: 150,
      imagen: 'assets/images/caminata.jpg'
    },
    {
      id: 2,
      nombre: 'Yoga',
      duracion: '45 minutos',
      calorias: 200,
      imagen: 'assets/images/yoga.jpg'
    }
  ];

  constructor() { }


  eliminarComida(id: number) {
    this.comidasFavoritas = this.comidasFavoritas.filter(comida => comida.id !== id);
  }

  eliminarEjercicio(id: number) {
    this.ejerciciosFavoritos = this.ejerciciosFavoritos.filter(ejercicio => ejercicio.id !== id);
  }
}