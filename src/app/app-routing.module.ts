/* app-routing.module.ts */

import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './services/auth.guard';
import { OnboardingGuard } from './services/onboarding.guard';
import { Tab3PageModule } from './tab3/tab3.module';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'onboarding',
    pathMatch: 'full'
  },
  {
    path: 'onboarding',
    loadChildren: () => import('./onboarding/onboarding.module').then(m => m.OnboardingPageModule),
    canActivate: [OnboardingGuard]
  },
  {
    path: 'register',
    loadChildren: () => import('./register/register.module').then(m => m.RegisterPageModule)
  },
  {
    path: 'login',
    loadChildren: () => import('./login/login.module').then(m => m.LoginPageModule)
  },
  {
    path: 'tabs',
    loadChildren: () => import('./tabs/tabs.module').then(m => m.TabsPageModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'tab3',
    component: Tab3PageModule
  },
  {
    path: 'progreso',
    loadChildren: () => import('./progreso/progreso.module').then( m => m.ProgresoPageModule)
  },
  {
    path: 'favoritos',
    loadChildren: () => import('./favoritos/favoritos.module').then( m => m.FavoritosPageModule)
  },
  {
    path: 'detalle-register',
    loadChildren: () => import('./detalle-register/detalle-register.module').then( m => m.DetalleRegisterPageModule)
  },
  { 
    path: 'recetas', 
    loadChildren: () => import('./recetas/recetas.module').then( m => m.RecetasPageModule)
   },
  {
    path: 'ejercicios', 
    loadChildren: () => import('./ejercicios/ejercicios.module').then( m => m.EjerciciosPageModule)
  },   {
    path: 'desafios',
    loadChildren: () => import('./desafios/desafios.module').then( m => m.DesafiosPageModule)
  },
  {
    path: 'tab3',
    loadChildren: () => import('./tab3/tab3.module').then(m => m.Tab3PageModule),
    canActivate: [OnboardingGuard]
  },
  {
    path: 'recursos',
    loadChildren: () => import('./recursos/recursos.module').then( m => m.RecursosPageModule)
  },
  {
    path: 'tips-enf-renal',
    loadChildren: () => import('./tips-enf-renal/tips-enf-renal.module').then( m => m.TipsEnfRenalPageModule)
  },
  {
    path: 'tips-hipotiroidismo',
    loadChildren: () => import('./tips-hipotiroidismo/tips-hipotiroidismo.module').then( m => m.TipsHipotiroidismoPageModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule]
})
export class AppRoutingModule {}