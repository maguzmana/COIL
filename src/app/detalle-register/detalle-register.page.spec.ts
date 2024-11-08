import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalleRegisterPage } from './detalle-register.page';

describe('DetalleRegisterPage', () => {
  let component: DetalleRegisterPage;
  let fixture: ComponentFixture<DetalleRegisterPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DetalleRegisterPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
