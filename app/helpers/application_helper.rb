module ApplicationHelper

	def validation_class(obj, class_name)
		class_name unless obj.new_record?
	end

end
