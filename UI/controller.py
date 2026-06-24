import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._categoria = None
        self._prod1 = None
        self._prod2 = None


    def fillDDCategoria(self):
        lista_categorie = self._model.getCategorie()
        for categoria in lista_categorie:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(data=categoria,
                                   key=categoria,
                                   text=categoria.category_name,
                                   on_click=self.read_category)
            )

    def read_category(self, e):
        if e.control.data is None:
            self._categoria= None
        else:
            self._categoria = e.control.data

    def handleCreaGrafo(self, e):

        if self._view._dp1.value is None or self._view._dp2.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserisci tutti i campi"))

        self._model.buildGraph(self._view._dp1.value, self._view._dp2.value, self._categoria.category_id)
        n, m = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo è costituito di {n} nodi ed {m} archi"))

        self._view._btnBestProdotti.disabled= False
        self._view.update_page()

        self._fillCampi()

    def _fillCampi(self):

        lista_nodi = self._model.getNodes()
        for nodo in lista_nodi:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(data=nodo,
                                   key=nodo,
                                   text=nodo.product_name,
                                   on_click=self.read_product1)
            )

        for nodo in lista_nodi:
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(data=nodo,
                                   key=nodo,
                                   text=nodo.product_name,
                                   on_click=self.read_product2)
            )

        self._view.update_page()

    def read_product1(self, e):
        if e.control.data is None:
            self._prod1= None
        else:
            self._prod1= e.control.data

    def read_product2(self, e):
        if e.control.data is None:
            self._prod2= None
        else:
            self._prod2= e.control.data

    def handleBestProdotti(self, e):

        classifica = self._model.getPiuVenduti()
        for nodo, score in classifica:
            self._view.txt_result.controls.append(
                ft.Text(f"{nodo.product_name} : {score}"))
        self._view.update_page()

    def handleCercaCammino(self, e):

        if self._view._txtInLun.value is None or self._prod1 is None or self._prod2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserisci tutti i campi"))
            self._view.update_page()
            return

        lun = int(self._view._txtInLun.value)
        if lun <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserisci un valore di lunghezza positivo maggiore di 0 "))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        cammino, score = self._model.getPath(self._prod1, self._prod2, lun)

        if len(cammino) != 0 and score != 0:
            for c in cammino:
                self._view.txt_result.controls.append(
                    ft.Text(f"{c.product_name}"))

            self._view.txt_result.controls.append(
                ft.Text(f"Peso complessivo massimo: {score}"))
            self._view.update_page()

        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino trovato con i dati inseriti"))

        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
