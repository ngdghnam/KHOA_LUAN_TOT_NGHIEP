import { Component, OnInit, computed } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Theme, ThemeService } from '../../core/services/theme.service';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css'],
  imports: [MatFormFieldModule, MatInputModule, MatButtonModule, MatTooltipModule, MatSelectModule],
})
export class NavBarComponent implements OnInit {
  constructor(readonly themeService: ThemeService) {}

  ngOnInit() {}

  themeLabel = computed(() => (this.themeService.currentTheme() === 'dark' ? 'Dark' : 'Light'));

  changeTheme(theme: Theme) {
    this.themeService.setTheme(theme);
  }
}
