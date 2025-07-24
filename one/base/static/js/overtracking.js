(function() {
    "use strict"; // Activa el modo estricto de JavaScript

    //Datos inciciales
    var collectedData = {
        ww: window.innerWidth,
        wh: window.innerHeight,
        t: 'pageview',
        u: window.location.href,
        r: document.referrer  || null,
        c: window.performance.getEntries().find(e => e.entryType === "navigation").responseStatus || null,
    };



    // Convierte el objeto a una cadena JSON
    var jsonData = JSON.stringify(collectedData);

    // Obtiene la URL del dominio donde se carga el JavaScript
    var targetURL = document.currentScript.src.replace('/t/t', '/t/p'); // Cambia "/path/to/api" por la ruta de tu API


function _sendData(data, type = 0) {
    const payload = JSON.stringify(data); // Convertir los datos a JSON

    // Crear un Blob con los datos codificados
    var blob = new Blob([data], { type: 'application/json; charset=UTF-8' });

    if (type === 1) {
        // Enviar directamente con XMLHttpRequest si type es 1
			const xhr = new XMLHttpRequest();
			xhr.open("POST", targetURL, true);
			xhr.setRequestHeader("Content-Type", "application/octet-stream");
			xhr.timeout = 10000;

			xhr.onload = function () {
				if (xhr.status >= 200 && xhr.status < 300) {

				}
			};

			xhr.onerror = function () {
				//console.error("Fallo de red con XMLHttpRequest");
			};

			xhr.ontimeout = function () {
				//console.error("La solicitud con XMLHttpRequest superÃ³ el tiempo lÃ­mite de 10 segundos.");
			};

			xhr.send(blob); // Enviar datos codificados
			return; // Salir despuÃ©s de enviar con XMLHttpRequest
		}

		// Intentar enviar con sendBeacon si type es 0
		try {
			const success = navigator.sendBeacon(targetURL, blob);
			if (success) {
				return; // Salir si el envÃ­o fue exitoso
			}
		} catch (error) {
			//console.warn("sendBeacon fallÃ³:", error);
		}

		// Respaldo con XMLHttpRequest
		const xhr = new XMLHttpRequest();
		xhr.open("POST", targetURL, true);
		xhr.setRequestHeader("Content-Type", "application/octet-stream");
		xhr.timeout = 10000;

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {

			} else {
				//console.error("Error en XMLHttpRequest:", xhr.status, xhr.statusText);
			}
		};

		xhr.onerror = function () {
			//console.error("Fallo de red con XMLHttpRequest");
		};

		xhr.ontimeout = function () {
			//console.error("La solicitud con XMLHttpRequest superÃ³ el tiempo lÃ­mite de 10 segundos.");
		};

		xhr.send(blob); // Enviar datos codificados
	}




    //enviamos los datos
    _sendData(jsonData);

    /**
     * ############################################
     * ########################  BUILDER :: BY LINK
     * ############################################
     */

    // FunciÃ³n principal para agregar el event listener a los enlaces que cumplen con la condiciÃ³n
    function builder_bylink_listeners(id_event, linkParameter, conditionParameter) {

        //Variables locales con prefijo "builder_bylink_"
        let builder_bylink_link = linkParameter;
        let builder_bylink_condition = conditionParameter;

        //FunciÃ³n para manejar el clic en un enlace
        function builder_bylink_handleClick(event) {
             //event.preventDefault();
            // Obtener el enlace pulsado
            const clickedLink = event.target.href || event.currentTarget.href;


            // Evaluar el condicional y enviar el JSON si cumple
            if (builder_bylink_evaluateCondition(clickedLink, builder_bylink_condition)) {
                const json = { i: id_event, t: 'event_bylink', u: window.location.href, l: clickedLink };
                const jsonData = JSON.stringify(json);

                _sendData(jsonData);
            }
        }

        //FunciÃ³n para evaluar el condicional
        function builder_bylink_evaluateCondition(text, condicional) {

            switch (condicional) {
                case 'same':
                    return text === builder_bylink_link;
                case 'startby':
                    return text.startsWith(builder_bylink_link);
                case 'endby':
                    return text.endsWith(builder_bylink_link);
                case 'contains':
                    return text.includes(builder_bylink_link);
                default:
                    return false;
            }
        }

        //Obtener solo los enlaces que cumplen con la condiciÃ³n
        const filteredLinks = Array.from(document.querySelectorAll('a')).filter(linkElement => builder_bylink_evaluateCondition(linkElement.href, builder_bylink_condition));

        //Agregar event listener solo a los enlaces filtrados
        filteredLinks.forEach(linkElement => {
            linkElement.addEventListener('click', builder_bylink_handleClick);
        });
    }

    /**
     * Custom GiaEvent
     */
    function _ovt(id_event, value = '') {
        const json = {
            i: id_event,
            t: 'event_custom',
            u: window.location.href,
            v: value
        };

        const jsonData = JSON.stringify(json);
        _sendData(jsonData);
    }



    // Expone la funciÃ³n _ovt al Ã¡mbito global asignÃ¡ndola al objeto window
    window._ovt = _ovt;

    /**
     * ############################################
     * ######################  BUILDER :: BY BUTTON
     * ############################################
     */

    //FunciÃ³n principal para agregar el event listener a los botones que cumplen con la condiciÃ³n
    function builder_bybutton_listeners(id_event, buttonText, conditionParameter) {

        // Variables locales con prefijo "builder_bybutton_"
        let builder_bybutton_text = buttonText;
        let builder_bybutton_condition = conditionParameter;

        // FunciÃ³n para manejar el clic en un botÃ³n
        function builder_bybutton_handleClick(event) {
            // Evitar el comportamiento predeterminado (evitar que cambie de pÃ¡gina)
            // event.preventDefault();

            // Obtener el texto plano del botÃ³n pulsado
            const clickedButtonText = event.target.innerText.replace(/<[^>]*>/g, ''); // Eliminar HTML si lo hay

            // Evaluar el condicional y enviar el JSON si cumple
            if (builder_bybutton_evaluateCondition(clickedButtonText, builder_bybutton_condition)) {
                const json = { i: id_event, t: 'event_bybutton', u: window.location.href, l: clickedButtonText };
                const jsonData = JSON.stringify(json);
                _sendData(jsonData);
            }
        }

        // FunciÃ³n para evaluar el condicional
        function builder_bybutton_evaluateCondition(text, condition) {
            switch (condition) {
                case 'same':
                    return text === builder_bybutton_text;
                case 'startby':
                    return text.startsWith(builder_bybutton_text);
                case 'endby':
                    return text.endsWith(builder_bybutton_text);
                case 'contains':
                    return text.includes(builder_bybutton_text);
                default:
                    return false;
            }
        }

        // Obtener solo los botones que cumplen con la condiciÃ³n
        const filteredButtons = Array.from(document.querySelectorAll('button')).filter(buttonElement => builder_bybutton_evaluateCondition(buttonElement.innerText.replace(/<[^>]*>/g, ''), builder_bybutton_condition));

        // Agregar event listener solo a los botones filtrados
        filteredButtons.forEach(buttonElement => {
            buttonElement.addEventListener('click', builder_bybutton_handleClick);
        });
    }

    /**
     * ############################################
     * #######################  BUILDER :: BY CLICK
     * ############################################
     */

    // FunciÃ³n principal para agregar el event listener a los elementos seleccionados por querySelector
    function builder_byclick_listeners(id_event, selector) {



        // Variable local con prefijo "builder_byclick_"
        let builder_byclick_selector = selector;

        // FunciÃ³n para manejar el clic en un elemento
        function builder_byclick_handleClick(event) {
            // Evitar el comportamiento predeterminado (evitar que cambie de pÃ¡gina)
            // event.preventDefault();

            // Realizar cualquier acciÃ³n deseada con el elemento clicado
            const clickedElement = event.target;

            // Enviar informaciÃ³n sobre el clic (por ejemplo, el selector del elemento)
            const json = { i: id_event, t: 'event_byclick', u: window.location.href, l: builder_byclick_selector };
            const jsonData = JSON.stringify(json);
            _sendData(jsonData);
        }

        //Check selector
        try {
            if (!document.querySelector(builder_byclick_selector)) { return false; }
        } catch (e) {
            return false;
        }

        // Obtener todos los elementos que coinciden con el selector
        const selectedElements = Array.from(document.querySelectorAll(builder_byclick_selector));

        // Agregar event listener a todos los elementos seleccionados
        selectedElements.forEach(element => {
            element.addEventListener('click', builder_byclick_handleClick);
        });
    }

    /**
     * ############################################
     * ######################  BUILDER :: BY SUBMIT
     * ############################################
     */

    // FunciÃ³n para agregar el event listener al formulario identificado por el selector
    function builder_byform_listeners(id_event, selector) {

        // Variable local con prefijo "builder_formsubmit_"
        let builder_formsubmit_selector = selector;

        // FunciÃ³n para manejar el envÃ­o del formulario
        function builder_formsubmit_handleSubmit(event) {
            // Evitar el comportamiento predeterminado del formulario (evitar el envÃ­o tradicional)
            //event.preventDefault();

            // Realizar cualquier acciÃ³n deseada con el formulario o sus datos antes de enviarlo
            const submittedForm = event.target;

            // Enviar informaciÃ³n sobre el envÃ­o del formulario (por ejemplo, el selector del formulario)
            const json = { i: id_event, t: 'event_byform', u: window.location.href, l: builder_formsubmit_selector };
            const jsonData = JSON.stringify(json);
            _sendData(jsonData);

            // Puedes enviar el formulario despuÃ©s de realizar las acciones deseadas
            //submittedForm.submit();
            //HTMLFormElement.prototype.submit.call(submittedForm);

        }

        //Check selector
        try {
            if (!document.querySelector(builder_formsubmit_selector)) { return false; }
        } catch (e) {
            return false;
        }

         // ContinÃºa con el cÃ³digo si el elemento existe.
        const targetForm = document.querySelector(builder_formsubmit_selector);

        // Verificar si se encontrÃ³ un formulario antes de agregar el event listener
        if (targetForm) { targetForm.addEventListener('submit', builder_formsubmit_handleSubmit); }
    }

    /**
     * ############################################
     * #########################  SCROLL
     * ############################################
     */

    //Set limits
	let ot_scroll = { max: 0 }; // Guardamos el mÃ¡ximo alcanzado
	let scrollTimeout; // Variable para el temporizador

	function ot_scroll_y() {

		// Obtenemos el tamaÃ±o de la pantalla y de la pÃ¡gina
		const windowHeight = window.innerHeight || (document.documentElement || document.body).clientHeight;
		const documentHeight = Math.max(
			document.body.scrollHeight,
			document.documentElement.scrollHeight,
			document.body.offsetHeight,
			document.documentElement.offsetHeight,
			document.body.clientHeight,
			document.documentElement.clientHeight
		);
		const scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
		const trackLength = documentHeight - windowHeight;
		const scroll = Math.floor((scrollTop / trackLength) * 100);

		// Solo ejecutamos si supera el mÃ¡ximo anterior
		if (scroll > ot_scroll.max) {
			ot_scroll.max = scroll; // Actualizamos el mÃ¡ximo
			clearTimeout(scrollTimeout); // Reiniciamos el temporizador si hay scroll continuo

			// Esperamos 2 segundos antes de enviar
			scrollTimeout = setTimeout(() => {
				const json = { t: 'event_scroll', u: window.location.href, l: ot_scroll.max };
				const jsonData = JSON.stringify(json);
				_sendData(jsonData);
			}, 2000);
		}
	}








	//Send load
	document.dispatchEvent(new Event('_ot_start'));


  })();
