/* tab2.page.ts */
import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-tab2',
  templateUrl: './tab2.page.html',
  styleUrls: ['./tab2.page.scss'],
})
export class Tab2Page implements OnInit {

  userName: string = 'Nombre de usuario';
  dailyTip: string = 'Consejo diario de salud';
  dailyTip2: string = 'Consejo diario'

  constructor(private navCtrl: NavController) { }

  ngOnInit() {
    // Inicializamos los valores
    this.userName = "Juan Carlos";  // Puedes cambiar este valor según corresponda
    this.dailyTip = "Come más frutas. Son ricas en fibra y te ayudarán a mantenerte saludable por más tiempo."; // Ejemplo de consejo diario
    this.dailyTip2 = "Recuerda que si sientes alguna molestia de salud debes consultar a tu doctor de confinza."; // Ejemplo de consejo diario
  }

  irAChatBot() {
    // Navega a tab1 donde está el chat bot
    this.navCtrl.navigateRoot('/tabs/tab1');
  }

}