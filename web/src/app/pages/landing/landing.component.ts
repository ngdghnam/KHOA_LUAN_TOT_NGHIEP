import { Component, OnDestroy, OnInit } from '@angular/core';
import { NavBarComponent } from '../../components/nav-bar/nav-bar.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { MatAnchor, MatButtonModule } from '@angular/material/button';
import { mockData } from '../../data';
import { Technologies } from '../../data/tech';
import { testimonials } from '../../data/testimonial';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css'],
  imports: [NavBarComponent, FooterComponent, MatAnchor, MatButtonModule, CommonModule],
})
export class LandingComponent implements OnInit, OnDestroy {
  mockData = mockData;
  technologies = Technologies;
  testimonials = testimonials;
  currentIndex = 1;
  carouselItems: any[] = [];
  autoplayInterval: any;
  itemWidth = 408;
  isTransitioning = true;

  constructor(private readonly router: Router) {}

  onClickScanCv() {
    this.router.navigate(['/scan-cv']);
  }

  ngOnInit() {
    this.setupCarousel();
    this.startAutoplay();
  }

  ngOnDestroy() {
    clearInterval(this.autoplayInterval);
  }

  setupCarousel() {
    const first = this.testimonials[0];
    const last = this.testimonials[this.testimonials.length - 1];

    this.carouselItems = [last, ...this.testimonials, first];
  }

  startAutoplay() {
    this.autoplayInterval = setInterval(() => {
      this.nextSlide();
    }, 1500);
  }

  nextSlide() {
    this.isTransitioning = true;
    this.currentIndex++;

    if (this.currentIndex === this.carouselItems.length - 1) {
      setTimeout(() => {
        this.isTransitioning = false;
        this.currentIndex = 1;
      }, 500);
    }
  }

  prevSlide() {
    this.isTransitioning = true;
    this.currentIndex--;

    if (this.currentIndex === 0) {
      setTimeout(() => {
        this.isTransitioning = false;
        this.currentIndex = this.carouselItems.length - 2;
      }, 500);
    }
  }
}
