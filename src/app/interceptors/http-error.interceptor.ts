import { Injectable } from '@angular/core';
import {
  HttpEvent, 
  HttpInterceptor, 
  HttpHandler, 
  HttpRequest,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {
  constructor(
    private alertController: AlertController,
    private router: Router
  ) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMessage = '';
        let errorTitle = 'Error';

        if (error.error instanceof ErrorEvent) {
          // Error del lado del cliente (red, etc.)
          errorMessage = `Error de conexión: ${error.error.message}`;
          this.handleClientError(errorMessage);
        } else {
          // Error del lado del servidor
          switch (error.status) {
            case 400:
              errorTitle = 'Error de Solicitud';
              errorMessage = error.error?.message || 'Solicitud incorrecta';
              break;
            case 401:
              errorTitle = 'No Autorizado';
              errorMessage = 'Sesión expirada. Por favor, inicie sesión nuevamente.';
              this.handleUnauthorizedError();
              break;
            case 403:
              errorTitle = 'Acceso Prohibido';
              errorMessage = 'No tiene permisos para realizar esta acción.';
              break;
            case 404:
              errorTitle = 'No Encontrado';
              errorMessage = 'El recurso solicitado no se encuentra disponible.';
              break;
            case 500:
              errorTitle = 'Error del Servidor';
              errorMessage = 'Ocurrió un error interno en el servidor.';
              break;
            case 0:
              errorTitle = 'Error de Conexión';
              errorMessage = 'No se pudo conectar con el servidor. Verifique su conexión a internet.';
              break;
            default:
              errorMessage = error.error?.message || `Código de estado: ${error.status}`;
          }

          // Log detallado del error
          this.logError(request, error, errorMessage);

          // Mostrar alerta de error
          this.showErrorAlert(errorTitle, errorMessage);
        }

        // Relanzar el error para que los componentes puedan manejarlo si es necesario
        return throwError(() => new Error(errorMessage));
      })
    );
  }

  // Método para manejar errores de cliente
  private handleClientError(message: string) {
    console.error('Error de cliente:', message);
  }

  // Método para manejar errores de autorización
  private handleUnauthorizedError() {
    // Limpiar token de autenticación
    localStorage.removeItem('token');
    
    // Redirigir a la página de login
    this.router.navigate(['/login']);
  }

  // Método para mostrar alerta de error
  private async showErrorAlert(title: string, message: string) {
    const alert = await this.alertController.create({
      header: title,
      message: message,
      buttons: ['OK']
    });

    await alert.present();
  }

  // Método para log detallado de errores
  private logError(
    request: HttpRequest<any>, 
    error: HttpErrorResponse, 
    errorMessage: string
  ) {
    console.group('HTTP Error Interceptor');
    console.error('URL de la solicitud:', request.url);
    console.error('Método HTTP:', request.method);
    console.error('Cuerpo de la solicitud:', request.body);
    console.error('Código de estado:', error.status);
    console.error('Mensaje de error:', errorMessage);
    console.error('Error completo:', error);
    console.groupEnd();
  }
}