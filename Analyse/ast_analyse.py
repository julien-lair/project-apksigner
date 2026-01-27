

with open("../apksigner/sources/com/android/apksig/internal/apk/ApkSigningBlockUtils.java", "r") as file:
    tree = jast.parse(file.read())


class NameVisitor(jast.JNodeVisitor):
    def visit_identifier(self, node):
        print(node)


visitor = NameVisitor()
visitor.visit(tree)