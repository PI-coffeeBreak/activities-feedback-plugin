import React, { useState } from "react";
import PropTypes from "prop-types";
import { FaStar, FaRegStar } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import { getApi } from "coffeebreak/event-app";
import { registerPluginTranslations } from "coffeebreak";
import en from "../locales/en.json";
import ptBR from "../locales/pt-BR.json";
import ptPT from "../locales/pt-PT.json";

const NS = "activities-feedback-plugin";
registerPluginTranslations(NS, { en, "pt-BR": ptBR, "pt-PT": ptPT });

export default function FeedbackFormComponent({
  activityId,
  title,
  description,
  submit_button,
  rating_scale,
  show_comment_box,
  initialRating = null,
  initialComment = ""
}) {
  const { t } = useTranslation(NS);
  const [rating, setRating] = useState(initialRating);
  const [hovered, setHovered] = useState(null);
  const [comment, setComment] = useState(initialComment);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    const feedbackData = {
      rating,
      comment
    };

    try {
      const api = getApi();
      let response;
      if (initialRating !== null || initialComment !== "") {
        response = await api.put(
          `/activities-feedback-plugin/feedback_activities/${activityId}`,
          feedbackData
        );
      } else {
        response = await api.post(
          `/activities-feedback-plugin/feedback_activities/${activityId}`,
          feedbackData
        );
      }

      if (response.status === 200 || response.status === 201) {
        setSuccess(true);
        setRating(null);
        setComment("");
        window.location.reload();
      } else {
        throw new Error(response.data?.detail || "Failed to submit feedback");
      }
    } catch (err) {
      console.error(err);
      if (err.response?.status === 422 && err.response?.data?.detail) {
        setError("Feedback has already been submitted for this activity.");
      } else {
        setError(`Erro: ${err.response?.data?.detail || err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feedback-form w-full max-w-lg mx-auto p-4 bg-base-100 rounded">
      <h2 className="text-2xl font-bold mb-2">{title?.text || t("form.title")}</h2>
      {description?.text && (
        <p className="mb-4 text-gray-700">{description.text || t("form.description")}</p>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium mb-1">
            {t("form.ratingLabel")}
          </label>
          <div className="flex gap-1 text-primary text-2xl">
            {Array.from({ length: rating_scale }, (_, i) => {
              const index = i + 1;
              return (
                <button
                  type="button"
                  key={index}
                  className="focus:outline-none hover:text-primary"
                  onClick={() => setRating(index)}
                  onMouseEnter={() => setHovered(index)}
                  onMouseLeave={() => setHovered(null)}
                >
                  {index <= (hovered || rating) ? <FaStar /> : <FaRegStar />}
                </button>
              );
            })}
          </div>
        </div>

        {show_comment_box && (
          <div>
            <label className="block bg-primary font-medium mb-1">
              {t("form.commentLabel")}
            </label>
            <textarea
              className="textarea textarea-bordered w-full"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder={t("form.commentPlaceholder")}
            />
          </div>
        )}

        <div className="text-right">
          <button type="submit" className="btn btn-primary rounded-xl" disabled={loading}>
            {loading ? t("form.submitting") : submit_button?.text || t("form.submit")}
          </button>
        </div>

        {success && (
          <div className="alert alert-success mt-4">
            {t("form.success")} {t("form.thankYou")}
          </div>
        )}
        {error && (
          <div className="alert alert-error mt-4">
            {error}
          </div>
        )}
      </form>
    </div>
  );
}

FeedbackFormComponent.propTypes = {
  activityId: PropTypes.number.isRequired,
  title: PropTypes.object,
  description: PropTypes.object,
  submit_button: PropTypes.object,
  rating_scale: PropTypes.number,
  show_comment_box: PropTypes.bool,
  require_auth: PropTypes.bool
};
