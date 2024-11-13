/* tab2-routing.module.ts */
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Tab2Page } from './tab2.page';

const routes: Routes = [
  {
    path: '',
    component: Tab2Page,
  },
  {
    path: 'nueva-pagina',  // Ruta a la nueva página
    loadChildren: () => import('../ejercicios/ejercicios.module').then(m => m.EjerciciosPageModule) // Asegúrate de que la página esté creada
  },
  {
    path: 'nueva-pagina',  // Ruta a la nueva página
    loadChildren: () => import('../tab3/tab3.module').then(m => m.Tab3PageModule) // Asegúrate de que la página esté creada
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class Tab2PageRoutingModule {}
