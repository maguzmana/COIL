import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DesafiosPage } from './desafios.page';
import { DesafiosSemanalesPage } from './semanales/desafios-semanales.page'; // Asegúrate de importar la página
import { DesafioGeneralPage } from './general/desafio-general.page'; // Asegúrate de importar la página

const routes: Routes = [
  {
    path: '',
    component: DesafiosPage
  },
  {
    path: 'semanales',
    component: DesafiosSemanalesPage
  },
  {
    path: 'general',
    component: DesafioGeneralPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DesafiosPageRoutingModule {}