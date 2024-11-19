import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TipsHipotiroidismoPage } from './tips-hipotiroidismo.page';

const routes: Routes = [
  {
    path: '',
    component: TipsHipotiroidismoPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TipsHipotiroidismoPageRoutingModule {}
