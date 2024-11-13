import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { DesafiosPageRoutingModule } from './desafios-routing.module';
import { DesafiosPage } from './desafios.page';
import { DesafiosSemanalesPage } from './semanales/desafios-semanales.page'; // Importa la página de desafíos semanales
import { DesafioGeneralPage } from './general/desafio-general.page'; // Importa la página de desafío general

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DesafiosPageRoutingModule
  ],
  declarations: [DesafiosPage, DesafiosSemanalesPage, DesafioGeneralPage] // Declara las páginas
})
export class DesafiosPageModule {}