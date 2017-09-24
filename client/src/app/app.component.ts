import {Subscription} from "rxjs/Subscription";
import { Component, ViewChild} from '@angular/core';
import {MediaChange, ObservableMedia} from "@angular/flex-layout";
import { MdSidenav } from "@angular/material";

@Component({
    moduleId: module.id,
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})

export class AppComponent {
    @ViewChild('sidenav') sidenav: MdSidenav;

    title = 'KSCRAPER!';

    constructor(public media: ObservableMedia) {}

    watcher: Subscription;
    isMobileView = false;

    ngOnInit():void {
        this.isMobileView = (this.media.isActive('xs') || this.media.isActive('sm'));

        this.watcher = this.media.subscribe((change:MediaChange) => {
            this.isMobileView = (change.mqAlias === 'xs' || change.mqAlias === 'sm');
        });
    }

    ngOnDestroy() {
        this.watcher.unsubscribe();
    }

    onLinkClick():void {
        if (this.isMobileView) {
            this.sidenav.close();
        }
    }

    openExternal(url:string):void{
        window.open(url, '_blank')
    }
}
