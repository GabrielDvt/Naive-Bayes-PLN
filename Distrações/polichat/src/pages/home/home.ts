import { Component } from '@angular/core';
import { NavController, LoadingController } from 'ionic-angular';
import { InAppBrowser } from '@ionic-native/in-app-browser';


@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController, public loadingCtrl: LoadingController, private iab: InAppBrowser) {

  	let loading = this.loadingCtrl.create({
	    content: 'Aguarde...'
	  });

  	loading.present();
  	const browser = this.iab.create('https://polichat.com.br/', '_self', "location=no,hideurlbar=yes,zoom=no");
  }

}
