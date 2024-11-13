import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-desafios',
  templateUrl: './desafios.page.html',
  styleUrls: ['./desafios.page.scss'],
})
export class DesafiosPage implements OnInit {

  challenges: any[] = []; // Aquí puedes almacenar los desafíos

  constructor() { }

  ngOnInit() {
    this.loadChallenges();
  }

  loadChallenges() {
    // Lógica para cargar desafíos según la condición física y logros del paciente
    this.challenges = [
      { title: 'Autosuperarse corriendo 2.2 km', description: 'Mejora tu marca personal.' },
      // Agrega más desafíos aquí
    ];
  }
}