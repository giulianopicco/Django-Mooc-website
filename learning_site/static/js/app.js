var DATATABLE_CONFIG = {
  responsive: true,
  "language": {
    "sProcessing": "Procesando...",
    "sLengthMenu": "Mostrar _MENU_ registros",
    "sZeroRecords": "No se encontraron resultados",
    "sEmptyTable": "Ningún dato disponible en esta tabla",
    "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
    "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
    "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
    "sInfoPostFix": "",
    "sSearch": "Buscar todo:",
    "sUrl": "",
    "sInfoThousands": ",",
    "sLoadingRecords": "Cargando...",
    "oPaginate": {
      "sFirst": "Primero",
      "sLast": "Último",
      "sNext": "Siguiente",
      "sPrevious": "Anterior"
    },
    "oAria": {
      "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
      "sSortDescending": ": Activar para ordenar la columna de manera descendente"
    }
  },
  "pageLength": 25,
  "order": []
};

var DATEPICKER_CONFIG = {
  language: 'es',
  format: 'dd/mm/yyyy'
};

var DATETIMEPICKER_CONFIG = {
  format: 'dd/mm/yyyy HH:ii',
  minuteStep: 30,
  autoclose: true,
  language: 'es',
};

var DATERANGEPICKER_CONFIG = {
  "buttonClasses": ["btn", "btn-sm"],
  "applyClass": "btn btn-success",
  "cancelClass": "btn btn-inverse",
  "locale": {
    "format": "DD/MM/YYYY",
    "separator": " - ",
    "applyLabel": "Aplicar",
    "cancelLabel": "Cancelar",
    "fromLabel": "De",
    "toLabel": "Hasta",
    "customRangeLabel": "Custom",
    "daysOfWeek": [
      "Dom",
      "Lun",
      "Mar",
      "Mier",
      "Jue",
      "Vier",
      "Sáb"
    ],
    "monthNames": [
      "Enero",
      "Febrero",
      "Marzo",
      "Abril",
      "Mayo",
      "Junio",
      "Julio",
      "Agosto",
      "Setiembre",
      "Octubre",
      "Noviembre",
      "Diciembre"
    ],
    "firstDay": 1
  }
};

var DROPIFY_CONFIG = {
  messages: {
    'default': 'Arrastre y suelte un archivo, o haga click aquí',
    'replace': 'Arrastre y suelte un archivo, o haga click aquí para reemplazar',
    'remove': 'Eliminar',
    'error': 'Ha ocurrido un error'
  },
  error: {
    'fileSize': 'El tamaño del archivo no puede ser mayor que {{ value }}.',
    'minWidth': 'El ancho de la imagen no puede ser menor que {{ value }}px.',
    'maxWidth': 'El ancho de la imagen no puede ser mayor que {{ value }}px',
    'minHeight': 'La altura de la imagen no puede ser menor que {{ value }}px.',
    'maxHeight': 'La altura de la imagen no puede ser mayor que {{ value }}px.',
    'imageFormat': 'El formato de imagen no es válido. Formatos aceptados: {{ value }}.',
    'fileExtension': 'Extensión del archivo no permitida. Extensiones aceptadas: {{ value }}'
  }
};

// $.fn.datetimepicker.dates['es'] = {
//   days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
//   daysShort: ["Dom", "Lu", "Mar", "Mier", "Jue", "Vie", "Sab"],
//   daysMin: ["Dom", "Lu", "Ma", "Mier", "Jue", "Vie", "Sab"],
//   months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
//     "Setiembre", "Octubre", "Noviembre", "Diciembre"],
//   monthsShort: ["En", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Agos", "Sep", "Oct", "Nov", "Dic"],
//   meridiem: '',
//   today: "Hoy",
//   clear: "Rensa"
// };

function setupForm(form) {
  $('[type=file]:not(.custom)', form).dropify(DROPIFY_CONFIG);
  $('input[type=text].input-daterange-datepicker:not(.custom)', form).daterangepicker(DATERANGEPICKER_CONFIG);
  $("select:not(.custom)", form).select2();
  $('input[type=text].datepicker:not(.custom)', form).datepicker(DATEPICKER_CONFIG);
  $('input[type=text].datetimeinput:not(.custom)', form).datetimepicker(DATETIMEPICKER_CONFIG);
}

function resizeImageToSpecificSize(el, width, height) {
  var file = $(el).get(0).files[0];
  if (!file || file.type.substring(0, 5) !== 'image')
    return;
  var reader = new FileReader();
  reader.onload = function(event) {
    var img = new Image();
    img.onload = function() {
      var oc = document.createElement('canvas'), octx = oc.getContext('2d');
      if (img.width > width || img.height > height) {
        oc.width = img.width;
        oc.height = img.height;
        octx.drawImage(img, 0, 0);
        if (img.width > width) {
          while (oc.width * 0.8 > width) {
            oc.width *= 0.8;
            oc.height *= 0.8;
            octx.drawImage(oc, 0, 0, oc.width, oc.height);
          }
          oc.width = width;
          oc.height = oc.width * img.height / img.width;
        } else if (img.height > height) {
          while (oc.width * 0.8 > width) {
            oc.width *= 0.8;
            oc.height *= 0.8;
            octx.drawImage(oc, 0, 0, oc.width, oc.height);
          }
          oc.width = width;
          oc.height = oc.width * img.height / img.width;
        }
        octx.drawImage(img, 0, 0, oc.width, oc.height);
      } else {
        oc.width = img.width;
        oc.height = img.height;
        octx.drawImage(img, 0, 0);
      }
      oc.toBlob(function (blob) {
        files[el.name] = blob;
      }, 'image/jpeg', 0.9);
    };
    img.src = event.target.result;
  };
  reader.readAsDataURL(file);
}

datatableview.defaults = $.extend(true, datatableview.defaults, DATATABLE_CONFIG);

datatableview.auto_initialize = true;

$(document).ready(function () {
  $('.data-table').DataTable(DATATABLE_CONFIG);
  //
  $('form').each(function () {
    setupForm($(this));
  });
});