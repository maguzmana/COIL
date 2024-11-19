// tab2.page.ts
import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-tab2',
  templateUrl: './tab2.page.html',
  styleUrls: ['./tab2.page.scss'],
})
export class Tab2Page implements OnInit {

  userName: string = 'Nombre de usuario';
  dailyTips: string[] = [
    'Come más frutas. Son ricas en fibra y te ayudarán a mantenerte saludable por más tiempo.',
    'Recuerda que si sientes alguna molestia de salud debes consultar a tu doctor de confianza.',
    'Hidratarte adecuadamente es crucial para la salud de tus riñones.',
    'Haz ejercicio regularmente para mantenerte en forma y mejorar tu bienestar general.',
    'Reduce el consumo de sal para evitar problemas de hipertensión.'
  ];
  dailyTip: string = '';  // El consejo que se mostrará actualmente
  currentTipIndex: number = 0;  // Índice para rotar los consejos

  constructor(private navCtrl: NavController) { }

  ngOnInit() {
    // Inicializamos el primer consejo
    this.dailyTip = this.dailyTips[this.currentTipIndex];
    this.startDailyTipRotation();  // Iniciar la rotación de los consejos
  }

  // Función para iniciar la rotación automática del consejo diario
  startDailyTipRotation() {
    setInterval(() => {
      this.currentTipIndex = (this.currentTipIndex + 1) % this.dailyTips.length;
      this.dailyTip = this.dailyTips[this.currentTipIndex];  // Actualizar el consejo
    }, 5000);  // Cambia el consejo cada 5 segundos
  }

  irAChatBot() {
    // Navega a tab1 donde está el chat bot
    this.navCtrl.navigateRoot('/tabs/tab1');
  }

}
