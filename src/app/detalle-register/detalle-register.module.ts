import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { DetalleRegisterPageRoutingModule } from './detalle-register-routing.module';

import { DetalleRegisterPage } from './detalle-register.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DetalleRegisterPageRoutingModule
  ],
  declarations: [DetalleRegisterPage]
})
export class DetalleRegisterPageModule {}
