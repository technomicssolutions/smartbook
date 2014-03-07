
var Menu = new Class({
    Implements: [Options],
    options:{
    	'menu_class': '.menu'
    },
    initialize: function(element) {
        this.element = element;
        this.menus = $$(this.options.menu_class);
        this.menus.each(function(menu, index){
        	menu.addEvents({
        		'mouseenter': function(){
                    if(menu.getElement('ul')){
                        menu.getElement('ul').setStyle('display', 'block');
                    }        			
			    },
			    'mouseleave': function(){
			    	if(menu.getElement('ul')){
                        menu.getElement('ul').setStyle('display', 'none');
                    }
    			}        	
        	});
        });
    },
    
});

window.addEvent('domready',function() {
	

	if($$('.menu_div').length > 0){
		new Menu($$('.menu_div')[0]);
	}
	
});

