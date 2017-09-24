import { Injectable, Inject} from '@angular/core';
import { Headers, Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import {DOCUMENT} from '@angular/platform-browser';
import { Post } from './post';
import { DownloadSource} from './download-source';

@Injectable()
export class PostService {
    private domain = 'http://localhost:5001'
    private api_root = this.domain+'/post';

    constructor(private http: Http, @Inject(DOCUMENT) private document) {
        this.api_root = document.location.protocol +'//'+ document.location.hostname + '/api/post';
    }

    getPostes() {
        let dummy = [
            new Post('test1', 'I write some shit'),
            new Post('test2', 'I write some more shit'),
        ];
        return Promise.resolve(dummy)

        // return this.http
        //     .get(this.api_root)
        //     .toPromise()
        //     .then(response => response.json() as Post[])
        //     .catch(this.handleError);
    }

    getPost(requestedPost: Post): Promise<Post> {
        return this.getPostes()
        .then(postes => postes.find(post => post.id === requestedPost.id));
    }

    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}
