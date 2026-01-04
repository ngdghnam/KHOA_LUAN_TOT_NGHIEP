import { Component, OnInit } from '@angular/core';
import { NavBarComponent } from '../../components/nav-bar/nav-bar.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { MatAnchor, MatButtonModule } from '@angular/material/button';
import { mockData } from '../../data';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css'],
  imports: [NavBarComponent, FooterComponent, MatAnchor, MatButtonModule],
})
export class LandingComponent implements OnInit {
  mockData = mockData;

  constructor() {}

  ngOnInit() {}
}
