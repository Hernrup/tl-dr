import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Post } from './post';
import { PostService } from './post.service';

@Component({
    moduleId: module.id,
    selector: 'post-list',
    templateUrl: 'post.component.html',
    styleUrls: ['post.component.css']
})
export class PostComponent implements OnInit {
    postes: Post[];
    error: any;
    loading: boolean = false;

    constructor(
        private router: Router,
        private postService: PostService,
    ) { }

    getPostes(): void {
        this.postService
        .getPostes()
        .then(postes => this.postes = postes)
        .catch(error => this.error = error);
    }


    ngOnInit(): void {
        this.getPostes();
    }

    onSelect(post: Post): void {
    }

}
