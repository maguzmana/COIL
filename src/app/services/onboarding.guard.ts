import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { OnboardingService } from './onboarding.service';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root'
})
export class OnboardingGuard implements CanActivate {
  constructor(
    private onboardingService: OnboardingService,
    private userService: UserService,
    private router: Router
  ) {}

  async canActivate(): Promise<boolean> {
    const hasSeenOnboarding = await this.onboardingService.hasSeenOnboarding();
    
    if (hasSeenOnboarding) {
      if (this.userService.isAuthenticated()) {
        this.router.navigate(['/tabs/tab2']);
      } else {
        this.router.navigate(['/login']);
      }
      return false;
    }
    
    return true;
  }
}