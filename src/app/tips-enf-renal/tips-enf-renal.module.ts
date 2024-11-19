import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { TipsEnfRenalPageRoutingModule } from './tips-enf-renal-routing.module';

import { TipsEnfRenalPage } from './tips-enf-renal.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TipsEnfRenalPageRoutingModule
  ],
  declarations: [TipsEnfRenalPage]
})
export class TipsEnfRenalPageModule {}
