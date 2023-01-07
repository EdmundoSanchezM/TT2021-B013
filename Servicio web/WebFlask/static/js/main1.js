/*Funcion de cargar*/
$(document).ready(function(){
    $(".button-collapse").sideNav(); //Menu del Header

    $('ul.tabs').tabs(); //Menu

    $('.parallax').parallax(); //Efecto Parallax

    $('.scrollspy').scrollSpy(); //Transicion a los elementos de forma fluida

    $('.modal-trigger').leanModal({ //Ventanas Modales (Las que aparecen derrepente :v)
          dismissible: true, // Afecto
          opacity: .7, // Opacidad de fondo
          in_duration: 300, // Duracion de la transicion al abrir
          out_duration: 250, // Duracion de la transicion al cerrar
        }
    );    

    Materialize.updateTextFields(); //Habilitar TextFields

    $('select').material_select(); //Habilitar los Select

    $('input#input_text, textarea#textarea1').characterCounter(); //Habilitar que Pueda Contar los Caracteres

    $('.datepicker').pickadate({ //Calendario
                selectMonths: true, // Habilitar la Seleccion de Meses
                selectYears: 15, // Numero de Años Posibles
                firstDay: true //Que el calendario empieze en lunes
            });

    $('.tooltipped').tooltip({delay: 50});//Mensajito en hover del boton

    $('.materialboxed').materialbox();//Efecto zoom de imagenes

    $('.NavLateral-DropDown').on('click', function(e){
        e.preventDefault();
        var DropMenu=$(this).next('ul');
        var CaretDown=$(this).children('i.NavLateral-CaretDown');
        DropMenu.slideToggle('fast');
        if(CaretDown.hasClass('NavLateral-CaretDownRotate')){
            CaretDown.removeClass('NavLateral-CaretDownRotate');    
        }else{
            CaretDown.addClass('NavLateral-CaretDownRotate');    
        }
         
    });
    
    $('.ShowHideMenu').on('click', function(){
        var MobileMenu=$('.NavLateral');
        if(MobileMenu.css('opacity')==="0"){
            MobileMenu.addClass('Show-menu');   
        }else{
            MobileMenu.removeClass('Show-menu'); 
        }   
    });

    $('.btn-ExitSystem').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro que deseas deslogearte?",   
            text: "Está a punto de salir del sistema",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Si, Estoy Seguro",
            animation: "slide-from-top",   
            closeOnConfirm: false,
            cancelButtonText: "Cancelar"
        }, function(){
            setTimeout(function(){ window.location='/login'; }, 200);
        });
    });

    $('.btn-EliminarAdmin').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Estas Seguro que Deseas Deslogearte?",   
            text: "Estas Apunto de Salir del Sistema",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Si, Estoy Seguro",
            animation: "slide-from-top",   
            closeOnConfirm: false,
            cancelButtonText: "Cancelar"
        }, function(){   
            window.location='login.html'; 
        });
    }); 

    $('.btn-Search').on('click', function(e){
        e.preventDefault();
        swal({   
            title: "¿Qué Deseas Buscar?",   
            text: "Escribe lo que deseas Buscar",   
            type: "input",   
            showCancelButton: true,   
            closeOnConfirm: false,   
            animation: "slide-from-top",   
            inputPlaceholder: "Escribe Aqui",
            confirmButtonText: "Buscar",
            cancelButtonText: "Cancelar" 
        }, function(inputValue){   
            if (inputValue === false) return false;      
            if (inputValue === "") {     swal.showInputError("Debes de Escribir algo");     
            return false   
            }      
            swal("¡Bien!", "Buscaremos Informacion relacionada con: " + inputValue, "success"); 
        });    
    });

    $('.btn-Notification').on('click', function(){
        var NotificationArea=$('.NotificationArea');
        if(NotificationArea.hasClass('NotificationArea-show')){
            NotificationArea.removeClass('NotificationArea-show');
        }else{
            NotificationArea.addClass('NotificationArea-show');
        }
    });

});