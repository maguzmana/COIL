import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DetalleRegisterPage } from './detalle-register.page';

const routes: Routes = [
  {
    path: '',
    component: DetalleRegisterPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DetalleRegisterPageRoutingModule {}
