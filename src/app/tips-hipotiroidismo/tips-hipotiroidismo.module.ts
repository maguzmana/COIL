import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { TipsHipotiroidismoPageRoutingModule } from './tips-hipotiroidismo-routing.module';

import { TipsHipotiroidismoPage } from './tips-hipotiroidismo.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TipsHipotiroidismoPageRoutingModule
  ],
  declarations: [TipsHipotiroidismoPage]
})
export class TipsHipotiroidismoPageModule {}
