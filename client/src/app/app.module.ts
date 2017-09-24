import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http, RequestOptions } from '@angular/http';
// import { AUTH_PROVIDERS } from 'angular2-jwt';
import { provideAuth, AuthHttp, AuthConfig } from 'angular2-jwt';

import './rxjs-extensions';
import { AppComponent } from './app.component';
import { routing, routedComponents } from './app.routing';
import { PostService } from './post.service';

import { MaterialModule } from '@angular/material';
import 'hammerjs';
import { FlexLayoutModule } from "@angular/flex-layout";
import {MdButtonModule, MdCheckboxModule, MdChipsModule, MdCardModule,
    MdToolbarModule, MdIconModule, MdMenuModule, MdListModule, MdTabsModule, MdSidenavModule, MdInputModule,
    MdGridListModule, MdProgressSpinnerModule} from '@angular/material';
import { PostListItemComponent } from './post-list-item/post-list-item.component';

export function authHttpServiceFactory(http: Http, options: RequestOptions) {
    return new AuthHttp( new AuthConfig({}), http, options);
}

@NgModule({
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        routing,
        HttpModule,
        MdButtonModule,
        MdChipsModule,
        MdCardModule,
        MdIconModule,
        MdToolbarModule,
        MdMenuModule,
        MdListModule,
        MdTabsModule,
        MdSidenavModule,
        MdInputModule,
        MdGridListModule,
        MdProgressSpinnerModule,
        FlexLayoutModule,
    ],
    declarations: [
        AppComponent,
        routedComponents,
        PostListItemComponent
    ],
    providers: [
        PostService,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
