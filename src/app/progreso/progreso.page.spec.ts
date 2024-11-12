import { ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';  // Importa el módulo de Ionic
import { ProgresoPage } from './progreso.page';

describe('ProgresoPage', () => {
  let component: ProgresoPage;
  let fixture: ComponentFixture<ProgresoPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProgresoPage ],
      imports: [ IonicModule.forRoot() ] // Asegúrate de importar el módulo Ionic
    })
    .compileComponents();  // Compila los componentes

    fixture = TestBed.createComponent(ProgresoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have selectedDate as a valid date string', () => {
    // Verifica que la fecha seleccionada sea una cadena válida
    expect(component.selectedDate).toBeTruthy();
    expect(new Date(component.selectedDate).getTime()).not.toBeNaN();
  });
});
