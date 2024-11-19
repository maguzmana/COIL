import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TipsEnfRenalPage } from './tips-enf-renal.page';

const routes: Routes = [
  {
    path: '',
    component: TipsEnfRenalPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TipsEnfRenalPageRoutingModule {}
