import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.dd_value = None

    def handle_create_graph(self, e):
        try:
            num_min = int(self._view.txtNumAlbumMin.value)
            self._model.build_graph(num_min)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {self._model._graph.number_of_edges()} nodi (artisti), {self._model._graph.number_of_edges()} nodi "))
            self._view.ddArtist.disabled = False
            self._view.btnArtistsConnected.disabled = False
            for nodo in self._model._graph.nodes():
                self._view.ddArtist.options.append(ft.dropdown.Option(key=nodo,text = self._model.dizionario_artisti[nodo]))
            self._view.update_page()
        except ValueError:
            self._view.show_alert("INSERIRE UN VALORE VALIDO")


    def change_artist(self,e):
        selected_key= int(self._view.ddArtist.value)

        for option in e.control.options:
            if option.key == selected_key:
                self.dd_value = option.key
                break


    def handle_connected_artists(self, e):
        try:
            artista = int(self.dd_value)

            lista = self._model.connected_artists(artista)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Artisti direttamente collegati all'artista {artista}, {self._model.dizionario_artisti[artista]}"))
            for tupla in lista:
                self._view.txt_result.controls.append(ft.Text(f"{tupla[0]}, {tupla[1]} - Numero di generi in comune {tupla[2]}"))


            self._view.txtMaxArtists.disabled = False
            self._view.txtMinDuration.disabled = False
            self._view.btnSearchArtists.disabled = False
            self._view.update_page()
        except ValueError:
            self._view.show_alert("INSERIRE UN VALORE VALIDO")


    def ric(self,e):
        try:
            artista = int(self.dd_value)
        except ValueError:
            self._view.show_alert("INSERIRE UN VALORE VALIDO")
            return
        try:
            min_duration = float(self._view.txtMinDuration.value)
        except ValueError:
            self._view.show_alert("INSERIRE UN VALORE VALIDO")
            return

        try:
            num_artisti = int(self._view.txtMaxArtists.value)
        except ValueError:
            self._view.show_alert("INSERIRE UN VALORE VALIDO")
            return

        if num_artisti <=0 or num_artisti>len(self._model.node):
            self._view.show_alert("INSERIRE UN VALORE VALIDO")

        peso,cammino = self._model.ricerca(artista,num_artisti,min_duration)

        self._view.txt_result.controls.clear()
        for c in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{c}, {self._model.dizionario_artisti[c]}"))

        self._view.txt_result.controls.append(ft.Text(f"Peso massimo {peso}"))

        self._view.update_page()





