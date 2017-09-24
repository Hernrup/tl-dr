import { Routes, RouterModule, CanActivate } from '@angular/router';

import { PostComponent } from './post.component';

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: '/posts',
    pathMatch: 'full'
  },
    {
    path: 'posts',
    component: PostComponent
  },
  ];

export const routing = RouterModule.forRoot(appRoutes);

export const routedComponents = [PostComponent];
